'use server';

import { revalidatePath } from 'next/cache';
import { connectToDatabase } from '../database/mongoose';
import { handleError } from '../utils';
import Image from '../database/models/image.model';
import User from '../database/models/user.model';
import { redirect } from 'next/navigation';
import { v2 as cloudinary } from 'cloudinary';

const populateUser = (query: any) =>
  query.populate({
    path: 'author',
    model: User,
    select: '_id firstName lastName clerkId',
  });

export async function addImage({ image, userId, path }: AddImageParams) {
  try {
    await connectToDatabase();

    const author = await User.findById(userId);

    if (!author) throw new Error('User not found');

    const newImage = await Image.create({ ...image, author: author._id });

    revalidatePath(path);

    return JSON.parse(JSON.stringify(newImage));
  } catch (error) {
    handleError(error);
  }
}

export async function updateImage({ image, userId, path }: UpdateImageParams) {
  try {
    await connectToDatabase();

    const imageToUpdate = await Image.findById(image._id);

    if (!imageToUpdate) throw new Error('Image not found');

    if (imageToUpdate.author.toHexString() !== userId) throw new Error('Unauthorized');

    const updatedImage = await Image.findByIdAndUpdate(imageToUpdate._id, image, { new: true });

    revalidatePath(path);

    return JSON.parse(JSON.stringify(updatedImage));
  } catch (error) {
    handleError(error);
  }
}

export async function deleteImage(imageId: string) {
  try {
    await connectToDatabase();

    await Image.findByIdAndDelete(imageId);
  } catch (error) {
    handleError(error);
  } finally {
    redirect('/');
  }
}

export async function getImageById(imageId: string) {
  try {
    await connectToDatabase();

    const image = await populateUser(Image.findById(imageId));

    if (!image) throw new Error('Image not found');

    return JSON.parse(JSON.stringify(image));
  } catch (error) {
    handleError(error);
  }
}

export async function getAllImages({
  limit = 9,
  page = 1,
  searchQuery = '',
}: {
  limit?: number;
  page: number;
  searchQuery?: string;
}) {
  try {
    await connectToDatabase();

    cloudinary.config({
      cloud_name: process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME,
      api_key: process.env.CLOUDINARY_API_KEY,
      api_secret: process.env.CLOUDINARY_API_SECRET,
      secure: true,
    });

    let expression = 'folder=imaginify';

    if (searchQuery) {
      expression += ` AND ${searchQuery}`;
    }

    const { resources } = await cloudinary.search.expression(expression).execute();

    const resourceIds = resources.map((resource: any) => resource.public_id);

    let query = {};

    if (searchQuery) {
      query = {
        publicId: {
          $in: resourceIds,
        },
      };
    }

    const skipAmount = (Number(page) - 1) * limit;
    const images = await populateUser(
      Image.find(query).sort({ updatedAt: -1 }).skip(skipAmount).limit(limit),
    );

    const totalImages = await Image.countDocuments(query);
    const savedImages = await Image.find().countDocuments();

    return {
      data: JSON.parse(JSON.stringify(images)),
      totalPage: Math.ceil(totalImages / limit),
      savedImages,
    };
  } catch (error) {
    handleError(error);
  }
}

export async function getUserImages({
  limit = 9,
  page = 1,
  userId,
}: {
  limit?: number;
  page: number;
  userId: string;
}) {
  try {
    await connectToDatabase();

    const images = await populateUser(
      Image.find({ author: userId })
        .sort({ createdAt: -1 })
        .limit(limit)
        .skip((page - 1) * limit),
    );

    const totalImages = await Image.countDocuments({ author: userId });

    return { data: JSON.parse(JSON.stringify(images)), totalPages: Math.ceil(totalImages / limit) };
  } catch (error) {
    handleError(error);
  }
}
