'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { createProfile } from '@/lib/api';
import { useAppStore } from '@/lib/store';
import { BrandVoice } from '@/lib/types';
import { cn, formatFileSize, isValidFileType } from '@/lib/utils';

// Validation schema
const profileSchema = z.object({
  company_name: z.string().min(3, 'Company name must be at least 3 characters').max(100),
  company_description: z.string().min(100, 'Description must be at least 100 characters').max(2000),
  brand_voice: z.nativeEnum(BrandVoice),
  brand_voice_custom: z.string().max(500).optional(),
}).refine((data) => {
  // If brand_voice is CUSTOM, custom text is required
  if (data.brand_voice === BrandVoice.CUSTOM && !data.brand_voice_custom) {
    return false;
  }
  return true;
}, {
  message: 'Custom brand voice description is required when "Custom" is selected',
  path: ['brand_voice_custom'],
});

type ProfileFormData = z.infer<typeof profileSchema>;

interface CompanyProfileFormProps {
  onSuccess?: () => void;
}

export default function CompanyProfileForm({ onSuccess }: CompanyProfileFormProps) {
  const setProfile = useAppStore((state) => state.setProfile);
  const existingProfile = useAppStore((state) => state.profile);

  const [files, setFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    reset,
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: existingProfile ? {
      company_name: existingProfile.company_name,
      company_description: existingProfile.company_description,
      brand_voice: existingProfile.brand_voice as BrandVoice,
      brand_voice_custom: existingProfile.brand_voice_custom,
    } : {
      brand_voice: BrandVoice.PROFESSIONAL,
    },
  });

  const brandVoice = watch('brand_voice');

  // File upload handlers
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    addFiles(droppedFiles);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      addFiles(selectedFiles);
    }
  };

  const addFiles = (newFiles: File[]) => {
    const allowedTypes = ['pdf', 'docx', 'txt'];
    const maxSize = 5 * 1024 * 1024; // 5MB

    const validFiles = newFiles.filter((file) => {
      // Check file type
      if (!isValidFileType(file, allowedTypes)) {
        setError(`File ${file.name} is not a supported type. Allowed: PDF, DOCX, TXT`);
        return false;
      }

      // Check file size
      if (file.size > maxSize) {
        setError(`File ${file.name} exceeds 5MB limit`);
        return false;
      }

      return true;
    });

    setFiles((prev) => [...prev, ...validFiles]);
    setError(null);
  };

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  // Form submission
  const onSubmit = async (data: ProfileFormData) => {
    setIsSubmitting(true);
    setError(null);
    setSuccess(false);

    try {
      const response = await createProfile(
        {
          company_name: data.company_name,
          company_description: data.company_description,
          brand_voice: data.brand_voice,
          brand_voice_custom: data.brand_voice === BrandVoice.CUSTOM ? data.brand_voice_custom : undefined,
        },
        files.length > 0 ? files : undefined
      );

      if (response.success) {
        // Save to Zustand store
        setProfile(response.profile);
        setSuccess(true);
        setFiles([]);

        // Call onSuccess callback if provided
        if (onSuccess) {
          setTimeout(() => onSuccess(), 1500);
        }
      } else {
        setError('Failed to create profile. Please try again.');
      }
    } catch (err: any) {
      console.error('Profile creation error:', err);
      setError(err.response?.data?.detail || err.message || 'An error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-3xl font-bold mb-6 text-gray-900">Company Profile</h2>

      {success && (
        <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg text-green-800">
          ✓ Profile created successfully!
        </div>
      )}

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Company Name */}
        <div>
          <label htmlFor="company_name" className="block text-sm font-medium text-gray-700 mb-2">
            Company Name *
          </label>
          <input
            {...register('company_name')}
            type="text"
            className={cn(
              'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
              errors.company_name ? 'border-red-500' : 'border-gray-300'
            )}
            placeholder="Enter your company name"
          />
          {errors.company_name && (
            <p className="mt-1 text-sm text-red-600">{errors.company_name.message}</p>
          )}
        </div>

        {/* Company Description */}
        <div>
          <label htmlFor="company_description" className="block text-sm font-medium text-gray-700 mb-2">
            Company Description * (100-2000 characters)
          </label>
          <textarea
            {...register('company_description')}
            rows={6}
            className={cn(
              'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
              errors.company_description ? 'border-red-500' : 'border-gray-300'
            )}
            placeholder="Describe your company, products, mission, target audience, and unique value proposition..."
          />
          {errors.company_description && (
            <p className="mt-1 text-sm text-red-600">{errors.company_description.message}</p>
          )}
        </div>

        {/* Brand Voice */}
        <div>
          <label htmlFor="brand_voice" className="block text-sm font-medium text-gray-700 mb-2">
            Brand Voice *
          </label>
          <select
            {...register('brand_voice')}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value={BrandVoice.PROFESSIONAL}>Professional</option>
            <option value={BrandVoice.CASUAL}>Casual</option>
            <option value={BrandVoice.EDGY}>Edgy</option>
            <option value={BrandVoice.INSPIRATIONAL}>Inspirational</option>
            <option value={BrandVoice.HUMOROUS}>Humorous</option>
            <option value={BrandVoice.CUSTOM}>Custom</option>
          </select>
        </div>

        {/* Custom Brand Voice */}
        {brandVoice === BrandVoice.CUSTOM && (
          <div>
            <label htmlFor="brand_voice_custom" className="block text-sm font-medium text-gray-700 mb-2">
              Custom Brand Voice Description *
            </label>
            <textarea
              {...register('brand_voice_custom')}
              rows={3}
              className={cn(
                'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                errors.brand_voice_custom ? 'border-red-500' : 'border-gray-300'
              )}
              placeholder="Describe your custom brand voice (e.g., 'Witty and sarcastic like a late-night comedian, but informative...')"
            />
            {errors.brand_voice_custom && (
              <p className="mt-1 text-sm text-red-600">{errors.brand_voice_custom.message}</p>
            )}
          </div>
        )}

        {/* File Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Upload Brand Documents (Optional)
          </label>
          <p className="text-sm text-gray-500 mb-3">
            Upload brand guidelines, pitch decks, or marketing materials (PDF, DOCX, TXT - max 5MB each)
          </p>

          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={cn(
              'border-2 border-dashed rounded-lg p-8 text-center transition-colors',
              isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-gray-50'
            )}
          >
            <input
              type="file"
              multiple
              accept=".pdf,.docx,.txt"
              onChange={handleFileInput}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <div className="text-gray-600">
                <p className="text-lg mb-2">📁 Drag & drop files here</p>
                <p className="text-sm">or <span className="text-blue-600 hover:text-blue-700 font-medium">browse</span></p>
              </div>
            </label>
          </div>

          {/* File List */}
          {files.length > 0 && (
            <div className="mt-4 space-y-2">
              {files.map((file, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">📄</span>
                    <div>
                      <p className="text-sm font-medium text-gray-900">{file.name}</p>
                      <p className="text-xs text-gray-500">{formatFileSize(file.size)}</p>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => removeFile(index)}
                    className="text-red-600 hover:text-red-700 font-medium text-sm"
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Submit Button */}
        <div className="flex gap-4">
          <button
            type="submit"
            disabled={isSubmitting}
            className={cn(
              'flex-1 px-6 py-3 rounded-lg font-medium text-white transition-colors',
              isSubmitting
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            )}
          >
            {isSubmitting ? 'Creating Profile...' : existingProfile ? 'Update Profile' : 'Create Profile'}
          </button>

          {existingProfile && (
            <button
              type="button"
              onClick={() => reset()}
              className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Reset
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
